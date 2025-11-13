import { DevicesPanel } from '#components/panels';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DevicesPanel', () => {
  let component: DevicesPanel;
  let fixture: ComponentFixture<DevicesPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DevicesPanel],
    }).compileComponents();

    fixture = TestBed.createComponent(DevicesPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
