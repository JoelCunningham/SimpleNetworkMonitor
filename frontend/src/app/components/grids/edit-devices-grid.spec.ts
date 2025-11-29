import { EditDevicesGrid } from '#components/grids';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('EditDevicesGrid', () => {
  let component: EditDevicesGrid;
  let fixture: ComponentFixture<EditDevicesGrid>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditDevicesGrid],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(EditDevicesGrid);
    component = fixture.componentInstance;

    // Set required input
    component.owner = { id: 1, name: 'Test Owner', devices: [] };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
