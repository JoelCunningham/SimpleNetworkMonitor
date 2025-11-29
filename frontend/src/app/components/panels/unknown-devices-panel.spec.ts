import { UnknownDevicesPanel } from '#components/panels';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('UnknownDevicesPanel', () => {
  let component: UnknownDevicesPanel;
  let fixture: ComponentFixture<UnknownDevicesPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnknownDevicesPanel],
    }).compileComponents();

    fixture = TestBed.createComponent(UnknownDevicesPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
