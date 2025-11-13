import { DeviceCard } from '#components/cards';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DeviceCard', () => {
  let component: DeviceCard;
  let fixture: ComponentFixture<DeviceCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceCard],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
